
#include "esp_camera.h"
#include "Arduino.h"
#include "FS.h"                // SD Card ESP32
#include "SD_MMC.h"            // SD Card ESP32
#include "soc/soc.h"           // Disable brownour problems
#include "soc/rtc_cntl_reg.h"  // Disable brownour problems
#include "driver/rtc_io.h"

int pictureNumber = 0;

int peso = 0;

unsigned long previousMillis = 0;     

const long interval = 5000;    

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); //disable brownout detector
 
  Serial.begin(115200);
  //Serial.setDebugOutput(true);
  //Serial.println();
  
    // Initialize the camera
  Serial.print("Initializing the camera module...");
  configESPCamera();
  Serial.println("Camera OK!");

  // Initialize the MicroSD
  Serial.print("Initializing the MicroSD card module... ");
  initMicroSDCard();
  
  writeFile(SD_MMC,"/log.txt","Peso de la balanza\n");
}

void loop() 
{

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) 
  {
    previousMillis = currentMillis;
      // Path where new picture will be saved in SD Card
    String path = "/Images/picture" + String(pictureNumber) +".jpg";
    savePhoto(path);
    pictureNumber +=1;
    String peso = "Peso" + String(pictureNumber)+ "\n";
    appendFile(SD_MMC,"/log.txt",peso.c_str());
  }

}
