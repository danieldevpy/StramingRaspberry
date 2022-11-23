// program to display time every 3 seconds



function showTime() {
    try {
            // return new date and time
        let dateTime= new Date();

        // returns the current local time
        let time = dateTime.toLocaleTimeString();
        let hr = document.getElementById("hora")
        hr.innerHTML = time;
        let imagem = document.getElementById("imagem")
        imagem.src = "./static/foto.jpeg"; 



        var src = $("#imagem").attr('src');

        if( src.indexOf('?') > 0 ) 
            src = src.substring( 0, src.indexOf('?') );

        var d = new Date();
        $("#imagem").attr("src", src + '?time=' + d.getTime() );


      } catch (error) {
        // bloco de tratamento do erro
        console.log('error')
      } 

      http://192.168.1.8:8080/view/templates/static/foto.jpeg

//     // display the time after 3 seconds
     setTimeout(showTime, 150);
}

// // calling the function
showTime();