$(function(){
    // si se cambio el numero
    $("#num_op").change(function(){
        var numero = $(this).val();
        // borro lo que esta dentro
        $('#respuestas').html('');
        // agrego los inputs nuevos
        
        for(var i=1; i <= numero; i++) {
            $('#respuestas')
                .append(`
                    <div class="form-group">
                        <label for="respuesta${i}">Opcion ${i}</label>
                        <textarea class="form-control" rows="3" name="op${i}" required></textarea>
                    </div>
                `)   
        }
	});
});