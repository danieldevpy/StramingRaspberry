class Streaming {
                constructor(id, ip, port) {
                  this.id = id;
                  console.log(id);
                  this.ws = new WebSocket(`ws://${ip}:${port}/cam`);
                  this.message = ''
                  this.facial = false
                  let image = document.getElementById("frame");
                  image.onload = function(){
                      URL.revokeObjectURL(this.src); // release the blob URL once the image is loaded
                  } 
                  this.ws.onmessage = function(event) {
                      image.src = URL.createObjectURL(event.data);
                      st.send();
                  };
                  this.ws.onclose = (event) => {
                    window.location.href = "/";
                  };
                }
                command(obj){
                        if (obj.style.backgroundColor != 'green'){
                            obj.style.backgroundColor = "green";
                        } else{
                            obj.style.backgroundColor = "white";
                        }
                        this.message = obj.name;
                    
            
                }
                send(){
                    this.ws.send(this.message)
                    this.message = ''
                   }
                desconect(){
                    this.message = 'exit'
                    this.ws.close();
 

                }
                
              }

          
