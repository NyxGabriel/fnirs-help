# fnirs-help
# Learn GLM  (often specifically for Turbo Satori (TS))

Video for a good start: [Why GLM?](https://www.youtube.com/watch?v=TrjQ9KPgZpE&t)

A very little bit more on the [Betas of GLM](https://www.youtube.com/watch?v=9VGX1ui4nFk)

#### Design Matrix 

##### Drift - many
These are changes that occur during the measuring session and are often related to external conditions during the scanning. From temperature to optode/electorde/superconductor drift, they need to be modeled because it really helps to clean the data  

This is part of the design matrix, usually a cosine that is related to how many conditions and what is the high pass value. 

##### Constant - 1
Constant noise is present in all of the data (colored noise ~mimics it)
##### Conditions: -however many 
**In TS**
> The coding of the triggers follows a very straightforward scheme: The first trigger (value 1) is always the rest or baseline condition and is used to declare the end of an active task condition. The values for the task conditions range from 2 to 10. 
>Much better when
>No task = 1
>Task = 2 

Otherwise, they take the value number 0,1,2,3... etc but always be careful when comparing estimates (betas) for conditions. Make you contrasts smart? 

###### Modeling functions 
**HRF** - 2gamma in our case,  it is the canonical one 
But there are options, also the paramters you pass the function (they are usually 6 params when modeling) are not the standard ones, which moves the peak and trough of the presumed BOLD response 

Typically the function is a 
**Boxcar** - square function that imitates the start and end of the condition over time


**Design matrix is the Convolved function of these functions (visually overlapping them but it is not obvious math, you do a Fourier transform on each and then multiply the values and then plot the new ones *I think*)**

##### Short Channels mean? - 2
>From MNE tuytorial: We also add the mean of the short channels to the design matrix. In theory, these channels contain only systemic components, so including them in the design matrix allows us to estimate the neural component related to each experimental condition uncontaminated by systemic effects

The signals captured by short channels mainly reflect changes in superficial layers, such as the skin and skull, rather than deep cerebral changes, Such systemic components include changes in blood pressure, heart rate, skin blood flow, etc. 

#### Preprocessed data 
Check other repository 
But from RAW fNIRS signal you basically just change to optical density  (? some magic is there)
Then to get HbO and HbDeO apply the Beer-Lambert Law
[**Beer-Labert Law**](https://en.wikipedia.org/wiki/Beer%E2%80%93Lambert_law) 
>A common and practical expression of the Beer-Lambert law relates the optical attenuation of a physical material containing a single attenuating species of uniform concentration to the optical path length through the sample and absorptivity of the species. This expression is:

$\ln(I_{0}/I)=A=\varepsilon \ell c$
where
A is the absorbance
$\varepsilon$  ε is the molar attenuation coefficient or absorptivity of the attenuating species
$\ell$ ℓ is the optical path length
c is the concentration of the attenuating species

In MNE you pass the $\ell$ parameter, but they call it The partial pathlength factor (ppf), it is a float. 
 

### Noise 
Colored noise 

 
Yhat - model, design matrix
X - data matrix

From video above
> In line , slope is changing, in glm - “shape” (HRF) is shrinking n growing 


### Software
[Nilearn](https://nilearn.github.io/dev/quickstart.html) - old but gold, basis of MNE GLM. Made for fMRI

