
#include <LSM6DS3.h>
#include <Wire.h>
#include <Kaya-project-1_inferencing.h>

#define CONVERT_TO_MS2    9.80665f
#define MAX_ACCEPTED_RANGE  2.0f

LSM6DS3 myIMU(I2C_MODE, 0x6A);

void setup() {
  
    Serial.begin(9600);
    while (!Serial);
    //Call .begin() to configure the IMUs
    if (myIMU.begin() != 0) {
        ei_printf("Device error");
    } else {
        ei_printf("Device OK!");
    }


}

float ei_get_sign(float number) {
    return (number >= 0.0) ? 1.0 : -1.0;
}

void loop() {
    ei_printf("\nStart Detecting in 2 seconds...\n");
 
    delay(2000);
 
    ei_printf("Sampling...\n");
 
    // IMU데이터 저장을 위한 버퍼
    float buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE] = { 0 };
 
    for (size_t i = 0; i < EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE; i += 3) {
        // 다음 틱을 감지
        uint64_t next_tick = micros() + (EI_CLASSIFIER_INTERVAL_MS * 1000);
 
        buffer[i] = myIMU.readFloatAccelX();
        buffer[i+1] = myIMU.readFloatAccelY();
        buffer[i+2] = myIMU.readFloatAccelZ();
        buffer[i+3] = myIMU.readFloatGyroX();
        buffer[i+4] = myIMU.readFloatGyroY();
        buffer[i+5] = myIMU.readFloatGyroZ();
        buffer[i+6] = myIMU.readTempC();
 
        for (int j = 0; j < 7; j++) {
            if (fabs(buffer[i + j]) > MAX_ACCEPTED_RANGE) {
                buffer[i + j] = ei_get_sign(buffer[i + j]) * MAX_ACCEPTED_RANGE;
            }
        }
 
        buffer[i + 0] *= CONVERT_TO_MS2;
        buffer[i + 1] *= CONVERT_TO_MS2;
        buffer[i + 2] *= CONVERT_TO_MS2;
        buffer[i + 3] *= CONVERT_TO_MS2;
        buffer[i + 4] *= CONVERT_TO_MS2;
        buffer[i + 5] *= CONVERT_TO_MS2;
        buffer[i + 5] *= CONVERT_TO_MS2;
        
 
        delayMicroseconds(next_tick - micros());
    }


    // 행위 분류를 위해 raw buffer를 signal로 변환
    signal_t signal;
    int err = numpy::signal_from_buffer(buffer, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, &signal);
    if (err != 0) {
        Serial.println("Failed to create signal from buffer (%d)\n", err);
        return;
    }
 
    // Run the classifier
    ei_impulse_result_t result = { 0 };
 
    err = run_classifier(&signal, &result, debug_nn);
    if (err != EI_IMPULSE_OK) {
        ei_printf("ERR: Failed to run classifier (%d)\n", err);
        return;
    }

    for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
      ei_printf("    %s: %.5f\n", result.classification[ix].label, result.classification[ix].value);
    }

    if(result.classification[0].value > 0.5){
      //UpDown
      ei_printf("UpDown");
      delay(2000);
    }else if(result.classification[1].value > 0.5){
      //LeftRight
      ei_printf("LeftRight");
      delay(2000);      
    }else{
      //idle
      ei_printf("Idle");
      delay(2000);
    }
}
