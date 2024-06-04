# hCaptcha-Solver
Simple program used to automate the solving of hCaptchas on sites such as discord.com

# Why Did I make This?
I created this program because I ahdnothing to do, I orignaly had it for personal use
I then decided to impliment it into some programs of mine before it's solve rate began to decrease
Once I saw this decrease I stopped working on it and now about 2 months later I've decided to add a few small updates
With these updates the solve rate should now be much higher, but not very good overall

# How Does This Work?
This works by using selenium to open a browser and go to an hcaptcha demo site where it opens the captcha
The program then clicks on the images it classifies as being correct based off what the prompt is
Due to hCaptcha's updates it is not working too well anymore, so feel free to contribute to the project

# How To Use It?
You can launch `start.bat` which opens command prompt and starts the `main.py`
If you would liek to change what website it solves captchas for, open `main.py` in any IDE or text editor
Please go down to line 35: ```driver.get('https://accounts.hcaptcha.com/demo')```
Replace: `https://accounts.hcaptcha.com/demo` with any site of your choice
The site the solver should solve captchas on must instantly display a captcha box
For example, if the site requires you to type information first, like a signup form, the solver wil not work
If you want to do something like make it solve after the form is filled out, you will need to impliment the solver into your code
You will then need to fill out the form, then have the program call the function you put the solver code into
Alertanitvely, you can simply put the solver into a class and do something like: ```from HCapSolver import solver```

# How To Retrain The Model?
You can retrain the capsolver by first opening `images.json`
You then need to add a new line, or edit an existing one and replace the two objects
The two objects should be objects that look very simialr, but are different, but don't get too specific
The objects should be simialr looking, but different because it helps teh model understand that a duck and a swan are different
Once you have the `images.json` fileld out you need to launch `imagescraper.py`
This program will automaticly scrape the web for images based off what you put in `images.json`
The program will put these images in `.../content/train/object1` & `.../content/train/object2`
Once you have all your training data images, you can launch `train.bat` which will start the `train.py` file
The `train.py` file will start going through all the different images and classifying them into different groups and set an index to each image group
You will then see the `class_indices.json` file and when you open it you will see a list of every folder within `.../content/train/` and a number 
There will also be a `model.keras` file which is used by the program to classify the images and then decide which class each image on the captcha belongs to

# CREDITS

Me, AG597

You can contact me on discord at `ag597` if you need anything
