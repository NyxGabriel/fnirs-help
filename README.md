# fnirs-help
# Learn GLM  (often speficially for Turbo Satori (TS))

Video for a good start: [Why GLM?](https://www.youtube.com/watch?v=TrjQ9KPgZpE&t)

A very little bit more on the [Betas of GLM](https://www.youtube.com/watch?v=9VGX1ui4nFk)

#### Design Matrix 
##### Conditions: 
**In TS**
> The coding of the triggers follows a very straightforward scheme: The first trigger (value 1) is always the rest or baseline condition and is used to declare the end of an active task condition. The values for the task conditions range from 2 to 10. 
>Much better when
>No task = 1
>Task = 2 

Otherwise they take the value number 0,1,2,3... etc but always be careful when comparing estimates (betas) for conditions. Make you contrasts smart? 

##### Modeling functions 
**HRF** - 2gamma in our case,  it is the canonical one 
But there are options, also the paramters you pass the function (they are usually 6 params when modeling) are not the standard ones, which moves the peak and trough of the presumed BOLD response 
**Boxcar** - square fucntion that imitates the start and end of the condition overtime

Design matrix is the Convolved function of these two (visually overlaping them but it is not obvisou math, you do a foruer transfform on each and then multuply the values and then plot the new ones *I think*)

 
Yhat - model, design matrix
X - data matrix

From video above
> In line , slope is changing, in glm - “shape” (HRF) is shrinking n growing 


