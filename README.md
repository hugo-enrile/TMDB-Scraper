<p align="center">
  <h1 align="center">TMDB-Scraper</h1>
</p> 
Implementation of a scraper in Python to obtain the title of the different episodes of all the seasons of a series entered by keyboard.

It currently supports the specification of different languages for the retrieval of chapters. It acts on the [TMDB website](https://www.themoviedb.org/), so the series that can be consulted are those registered on that site.

# Languages
The languages currently supported are:

* English
* Spanish
* German
* French
* Italian
* Portuguese

# How it works
Once the script is executed, the user is asked to enter the title of the series he/she wants to consult. The user is then asked to specify the desired language for the titles of the episodes of the series.

Finally, the titles of the episodes are displayed on the screen, broken down by season.

# Requirements
In requierements.txt it is possible to check the libraries needed to run the script. It is recommended for a correct execution of the program that the webdriver.exe file that uses the Selenium library is located in the same directory from which the script is launched.
