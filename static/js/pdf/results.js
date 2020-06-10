document.write("<"+"script type='text/javascript' src='../static/js/pdf/imagen.js'><"+"/script>")

$(function(){
	$('.pdf').click(function(){
      var clases = $(this).attr("class");
      var listaDeClases = clases.split(' ');
      var idVoting = listaDeClases[3]
      obtenerMensaje(idVoting)
   });
});

function obtenerMensaje(idVoting) {
    var form = $('#form'+idVoting);
	$.ajax({ 
        url: '/management/voting_results/' + idVoting,
        type: 'POST',
        data: form.serialize(),
        success : function(data) {
            var votacion = data.votacion
            var users = data.users;
            var results = data.results;
            var fecha = data.fecha;
            pdfVotantes(votacion,users,results,fecha);
        }
    });
}

function pdfVotantes(votacion,users,results,fecha){
    //obtener buen formato para fecha
    var fechaArreglo = fecha.split('-');
    var year=fechaArreglo[0];
    var mes = obtenerMes(fechaArreglo[1]);
    var aux=fechaArreglo[2].split('T');
    var dia = aux[0];
    var auxHora=aux[1].split(':');
    //---------------------ra------
    var url=regresarImagen();
    var contenido=[];
    var bodyVotantes=[];
    var bodyResults=[];
    bodyVotantes.push([{text:'Nombre',color : 'white',alignment: 'center', style: 'pregunta'}, {text:'# Empleado',color : 'white',alignment: 'center', style: 'pregunta'},{text:'Delegación',color : 'white',alignment: 'center', style: 'pregunta'}]);
    //para sacar el contenido del body que esla tabla de votantes
    for (var i=0; i < users.length; i++) {
          bodyVotantes.push([{text:users[i].nombre_completo, style: 'texto'}, {text: users[i].numero_de_empleado,alignment: 'center', style: 'texto'}, {text:users[i].delegacion, style: 'texto'}]);
    }
    //para sacar el contenido del body que esla tabla de votantes
    bodyResults.push([{text:'Opción',alignment: 'center',color : 'white', style: 'pregunta'}, {text:'Cantidad de votos',color : 'white',alignment: 'center', style: 'pregunta'}]);
    for (var i=0; i < results.length; i++) {
        bodyResults.push([{text:results[i].respuesta, style: 'texto'},{ text: results[i].votos ,alignment: 'center', style: 'texto'}]);
    }
    //encabezado
    contenido.push({
      columns: 
      [
            
            
            {
                  // usually you would use a dataUri instead of the name for client-side printing
                  // sampleImage.jpg however works inside playground so you can play with it
                  image: url,
                  width: 60,
                  height:60,
                  margin: [ 0,0,0,0 ]
            },
            { width: 430,
                  text: 'SINDICATO DE TRABAJADORES ACADÉMICOS DE LA UNIVERSIDAD DE SONORA',alignment: 'center',color: '#A73B30',margin: [ 10,5,0,0 ],bold: true,fontSize: 20}
      ]
    },);
    //contenido.push({ text: 'SINDICATO DE TRABAJADORES ACADÉMICOS DE LA UNIVERSIDAD DE SONORA',alignment: 'center',color: '#A73B30',margin: [ 80,0,0,0 ],bold: true,fontSize: 20});
    contenido.push({ text: "\n\nRESULTADOS DE LA VOTACIÓN (prueba piloto)\n\n",alignment: 'center', style: 'titulo'});
    contenido.push({ text: votacion.tema + "\n\n",alignment: 'center', style: 'tema'});
    contenido.push({ text: votacion.pregunta + "\n\n\n", style: 'pregunta'});
    //aqui agregar los resultados
    contenido.push({
        margin: [30, 0, 0, 0],
        style: 'tableExample',
        color: '#444',
        table: {
            widths: [200,200],
            //headerRows: 1,
            // keepWithHeaderRows: 1,
            body: bodyResults
        },
        layout: {
            fillColor: function (i, node) {
                    //pinta el titulo de rojo mas oscuro
                    if(i==0)return '#A73B30';
            }
        }
    });
    //terminan de agregear los resultados y empieza a agregar al tabla
    contenido.push({ text: '', pageBreak:'after'});
    //contenido.push({ text: 'SINDICATO DE TRABAJADORES ACADÉMICOS DE LA UNIVERSIDAD DE SONORA',alignment: 'center',color: '#A73B30',margin: [ 80,0,0,0 ],bold: true,fontSize: 20});
    //encabezado
    contenido.push({
      columns: 
      [
            
            
            {
                  // usually you would use a dataUri instead of the name for client-side printing
                  // sampleImage.jpg however works inside playground so you can play with it
                  image: url,
                  width: 60,
                  height:60,
                  margin: [ 0,0,0,0 ]
            },
            { width: 430,
                  text: 'SINDICATO DE TRABAJADORES ACADÉMICOS DE LA UNIVERSIDAD DE SONORA',alignment: 'center',color: '#A73B30',margin: [ 10,5,0,0 ],bold: true,fontSize: 20}
      ]
    },);
    contenido.push({ text: "\n\nPARTICIPANTES EN LA VOTACIÓN (prueba piloto)\n\n",alignment: 'center', style: 'titulo'});
    contenido.push({ text: votacion.tema + "\n\n",alignment: 'center', style: 'tema'});
    contenido.push({
        style: 'tableExample',
        color: '#444',
        table: {
            widths: [200,100,200],
            dontBreakRows: true,
            //headerRows: 1,
            // keepWithHeaderRows: 1,
            body: bodyVotantes
        },
        layout: {
            fillColor: function (i, node) {
                    //pinta el titulo de azul mas oscuro
                    if(i==0)return '#A73B30';
            }
        }
    });
    
    var docDefinition = { 
        /*header: {
            margin: [ 40,40,10,60 ],
            columns: [
                  {
                     // usually you would use a dataUri instead of the name for client-side printing
                     // sampleImage.jpg however works inside playground so you can play with it
                     image: url,
                     width: 60,
                     height:60
                  },
                  {
                  }
            ]
       },*/ 
       content: contenido,  
       footer: { text: 'Hermosillo, Sonora a ' + dia + " de "+mes+" del "+year+".",alignment: 'center',fontSize: 10,margin: [0, 13, 0, 13] },  
       styles: {
          titulo: {
                fontSize: 16,
                margin: [0, 5, 0, 5]
          },
          tema: {
                fontSize: 14,
                bold: true,
                margin: [0, 5, 0, 5]
          },
          pregunta: {
            fontSize: 11,
            bold: false,
            margin: [0, 5, 0, 5],
            alignment: 'justify'
          },
          texto: {
            fontSize: 10,
            bold: false,
            margin: [5, 5, 0, 5]
          }
       },
       resaltar: {
          bold: true
       },
       defaultStyle: {
          fontSize: 14,
          alignment: 'left'
       },
       pageMargins: [ 50,50,50,50 ],
       pageSize: 'LETTER',
    };
    pdfMake.createPdf(docDefinition).download('resultados.pdf');
}

//funcion para obtener en letra el mes obtenido
function obtenerMes(mes){
    switch(mes) {
          case '01':
                mes='Enero';
                break;
          case '02':
                mes='Febrero';
                break;
          case '03':
                mes='Marzo';
                break;
          case '04':
                mes='Abril';
                break;
          case '05':
                mes='Mayo';
                break;
          case '06':
                mes='Junio';
                break;
          case '07':
                mes='Julio';
                break;
          case '08':
                mes='Agosto';
                break;
          case '09':
                mes='Septiembre';
                break;
          case '10':
                mes='Octubre';
                break;
          case '11':
                mes='Noviembre';
                break;
          case '12':
                mes='Diciembre';
                break;
    }
    return mes;
}