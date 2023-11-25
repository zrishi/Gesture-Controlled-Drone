        
#include <PWM.h>;
const int HeightPin =  9;      // The pin used to control the height
const int PitchPin =  10;      // The pin used to control the move along x-axis
const int RollPin =  5;      // The pin used to control the move along y-axis
const int YawPin =  3;
int i=0;
int Value=92;
int HeightValue=0;
int PitchValue=0;
int RollValue=0;
int YawValue=0;
int startflag=0;
void setup() {
pinMode(HeightPin, OUTPUT); 
pinMode(PitchPin, OUTPUT); 
pinMode(RollPin, OUTPUT); 
pinMode(YawPin, OUTPUT);

InitTimers();

InitTimersSafe();

SetPinFrequency(HeightPin,1000);
SetPinFrequency(PitchPin,1000);
SetPinFrequency(RollPin,1000);
SetPinFrequency(YawPin,1000);

pwmWrite(HeightPin,85);
pwmWrite(RollPin,82);
pwmWrite(YawPin,81);
pwmWrite(PitchPin,82);
// Initialize serial port
Serial.begin(9600);
}

void loop() {
 if (Serial.available() > 0) 
    {
      if(startflag==0)
      {
        SetPinFrequency(HeightPin,10000);
        SetPinFrequency(PitchPin,10000);
        SetPinFrequency(RollPin,10000);
        SetPinFrequency(YawPin,10000);
        startflag=1;
      }
      char Command=Serial.read();
       if(Command == 'S')
      {
        pwmWrite(HeightPin,140); 
        pwmWrite(YawPin,165);
        pwmWrite(RollPin,165);
        pwmWrite(PitchPin,25);  
        
       }
      if(Command == 'H')
      {
        SetPinFrequency(HeightPin,10000);
        SetPinFrequency(PitchPin,10000);
        SetPinFrequency(RollPin,10000);
        SetPinFrequency(YawPin,10000);
        pwmWrite(HeightPin,86);
        pwmWrite(RollPin,82);
        pwmWrite(YawPin,81);
        pwmWrite(PitchPin,82);        
        // for(i=165;i>=81;i--)
        // {
        //      pwmWrite(YawPin,i); 
        // }
        // for(i=140;i>=86;i--)
        // {
        //      pwmWrite(HeightPin,i); 
        // }
        // for(i=165;i>=82;i--)
        // {
        //      pwmWrite(RollPin,i);
        // }
        // for(i=25;i<=82;i++)
        // {
        //     pwmWrite(PitchPin,i); 
        // }
      }      
      if(Command == 'U')
       {
        pwmWrite(HeightPin,0);
        pwmWrite(RollPin,82);
        pwmWrite(YawPin,81);
        pwmWrite(PitchPin,82);            
       }
      if(Command == 'D')
       {
        pwmWrite(HeightPin,165);
        pwmWrite(RollPin,83);
        pwmWrite(YawPin,82);
        pwmWrite(PitchPin,83);

        //  delay(1000);

        // for(i=165;i>0;i--){
        // pwmWrite(HeightPin,i);          
        // }
        // for(i=83;i>0;i--){
        // pwmWrite(RollPin,i);          
        // }
        // for(i=82;i>0;i--){
        // pwmWrite(YawPin,i);          
        // }
        // for(i=83;i>0;i--){
        // pwmWrite(PitchPin,i);          
        // }
       }
       if(Command == 'F')
       {
        pwmWrite(HeightPin,84);
        pwmWrite(RollPin,82);
        pwmWrite(YawPin,81);
        pwmWrite(PitchPin,165);            
       }
       if(Command == 'B')
       {
        pwmWrite(HeightPin,84);
        pwmWrite(RollPin,82);
        pwmWrite(YawPin,81);
        pwmWrite(PitchPin,0);            
       }
       if(Command == 'L')
       {
        pwmWrite(HeightPin,84);
        pwmWrite(RollPin,0);
        pwmWrite(YawPin,81);
        pwmWrite(PitchPin,82);            
       }
      if(Command == 'R')
       {
        pwmWrite(HeightPin,84);
        pwmWrite(RollPin,165);
        pwmWrite(YawPin,81);
        pwmWrite(PitchPin,82);            
       }  
      //  if(Command == 'T')
      //  {
      //   pwmWrite(HeightPin,84);
      //   pwmWrite(RollPin,82);
      //   pwmWrite(YawPin,165);
      //   pwmWrite(PitchPin,82);            
      //  }  
      //  if(Command == 'V')
      //  {
      //   pwmWrite(HeightPin,84);
      //   pwmWrite(RollPin,82);
      //   pwmWrite(YawPin,0);
      //   pwmWrite(PitchPin,82);            
      //  }              

      // Stop is received
    }
}

