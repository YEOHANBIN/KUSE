// CAN Receive Example
//

#include <mcp_can.h>
#include <SPI.h>
#include <Servo.h>

int LED1 = 8;
int LED2 = 9;
int buzzer = 4;
int pos = 0;
bool flag = true;
int dis = 0;
long unsigned int rxId;
unsigned char len = 0;
unsigned char rxBuf[8];
char msgString[128];                        // Array to store serial string

#define CAN0_INT 2                              // Set INT to pin 2
MCP_CAN CAN0(10);                               // Set CS to pin 10
Servo myservo;

void setup()
{
  Serial.begin(115200);
  
  // Initialize MCP2515 running at 16MHz with a baudrate of 500kb/s and the masks and filters disabled.
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_16MHZ) == CAN_OK)
    Serial.println("MCP2515 Initialized Successfully!");
  else
    Serial.println("Error Initializing MCP2515...");
  
  CAN0.setMode(MCP_NORMAL);                     // Set operation mode to normal so the MCP2515 sends acks to received data.

  pinMode(CAN0_INT, INPUT);                            // Configuring pin for /INT input
  myservo.attach(7);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  Serial.println("MCP2515 Library Receive Example...");
}


void loop()
{
  if(!digitalRead(CAN0_INT))                         // If CAN0_INT pin is low, read receive buffer
  {
    CAN0.readMsgBuf(&rxId, &len, rxBuf);      // Read data: len = data length, buf = data byte(s)
    
    if((rxId & 0x80000000) == 0x80000000)     // Determine if ID is standard (11 bits) or extended (29 bits)
      sprintf(msgString, "Extended ID: 0x%.8lX  DLC: %1d  Data:", (rxId & 0x1FFFFFFF), len);
    else
      sprintf(msgString, "Standard ID: 0x%.3lX       DLC: %1d  Data:", rxId, len);
  
    Serial.print(msgString);
  
    if((rxId & 0x40000000) == 0x40000000){    // Determine if message is a remote request frame.
      sprintf(msgString, " REMOTE REQUEST FRAME");
      Serial.print(msgString);
    } else {
      for(byte i = 0; i<len; i++){
        sprintf(msgString, " 0x%.2X", rxBuf[i]);
        Serial.print(msgString);
      }

      if(rxId == 0x12)
      {
        int32_t distance = rxBuf[7];
        distance = (distance<<8)|rxBuf[6];
        dis = distance;
        if((distance > 7)&&(distance < 15)){
          digitalWrite(LED2, HIGH);
          tone(buzzer, 1000);
          delay(1000);
          noTone(buzzer);
          delay(1000);
        }
        else if(distance<=7){
          if(rxBuf[5] == 0){
            digitalWrite(LED2, HIGH);
            tone(buzzer, 1000);
            delay(50);
            digitalWrite(LED2, LOW);
            noTone(buzzer);
            delay(50);
          }
          else{
            digitalWrite(LED2, HIGH);
            tone(buzzer, 1000);
            delay(50);
            noTone(buzzer);
            delay(50);
          }
        }
        else 
        {digitalWrite(LED2, LOW);
        noTone(buzzer);
        }
      }
      if(rxId == 0x34)
      {
        if(rxBuf[1]<40) digitalWrite(LED1, HIGH);
      }
      else digitalWrite(LED1, LOW);

    
      if(dis <10){
	      pos += 0;}
      else{
	      if(flag == true) pos += 1;
	      else pos -= 1;}
      myservo.write(pos);
      if (pos >= 180) flag = false;
      else if (pos <= 0) flag = true;
    }

        
    Serial.println();
  }
}

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
