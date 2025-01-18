# Broker MQTT para IoT en AWS EC2

Se va a implementar un broker MQTT que reciba datos de un ESP32 y los almacene en un archivo CSV

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)
![espressiff](https://img.shields.io/badge/espressif-E7352C?style=for-the-badge&logo=espressif&logoColor=white)

<hr>

Vamos al servicio AWS EC2. 

   Creamos un grupo de seguridad con las siguientes configuraciones.      
      
   - Name: broker-mqtt-SG
   - Inboud rules:
      - Type: Custom TCP
         - Port Range: 1883
         - Source: 0.0.0.0/0
      - Type: ssh
         - Port Range: 22
         - Source: myIP        
      
   Creamos una instancia EC2 donde vamos a configurar el broker MQTT. La instancia tiene las siguientes configuraciones:
   
   - AMI: *Ubuntu*
   - Instance Type: *t2.micro*
   - Key Pair: associate a key pair
   - Network settings:
     - VPC
     - Public Subnet: enable *Public IP*
     - Security Group: broker-mqtt-SG
     - Advanced details:

     - User data: *copy the next following lines to the user data*
          
                    #!/bin/bash
                    sudo apt update
                    sudo apt install mosquitto mosquitto-clients           
                    sudo systemctl start mosquitto           
                    sudo systemctl enable mosquitto           
                    
            
   Una vez que la instancia se está ejecutando puedes conectarte a través de SSH y comprobar que las librerías se han instalado.

   Se debe agregar los siguiente al archivo de configuración que está en la ruta /etc/mosquitto/mosquitto.conf

                      allow_anonymous true #allow connection without authentication 
                      listener 1883 #allow connection from every ip
    
    Se puede probar el broker abriendo otro terminal y ejecutando lo siguiente:

                      mosquitto_pub -h ip-address -p 1883 -t "test/topic" -m "Hello from MQTT client"