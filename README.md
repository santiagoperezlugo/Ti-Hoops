# Hoops-Analytics

<img width="1469" alt="Screenshot 2024-07-08 at 7 54 00 PM" src="https://github.com/santiagoperezlugo/Hoops-Analytics/assets/144164736/c8b66fd4-efbf-4990-b2c4-ad0c30ae5c47">

## Introduction
Hoops-Analytics harnesses the power of deep learning to succesfully predict 66% of over 50,000 NBA games correctly, and with an average distance of 8 points from the true score. Built using PyTorch, this platform uses a neural network model which features layers of linear transformations, ReLU activations, batch normalization, and dropout to mitigate overfitting. This allows the model to learn complex patterns and dependencies in 47 years of NBA data, optimizing predictions through an Adam optimizer and SmoothL1Loss for refined accuracy.


# To Play
[ti-hoops.com](http://ti-hoops.com)

# To Build:

## Prerequisites
- Python 3.8+
- MySQL Server

### Installation

a 
```bash
git clone https://github.com/santiagoperezlugo/Ti-Hoops.git
```

b. 
```bash
pip3 install -r requirements.txt
```

### Set Environment Variables in Your Session:
```bash
export HOST='127.0.0.1'

export USER="root"

export PASSWORD="your_password"

export NAME="nba_data"
```
### Training the Model

To train the model, run
```bash
python src/main.py
```

## Example Terminal Output: 

<img width="663" alt="Screenshot 2024-07-08 at 7 39 51 PM" src="https://github.com/santiagoperezlugo/Hoops-Analytics/assets/144164736/af358bc8-16e7-40bd-9b11-773c05162163">

### Usage

Load the dependencies: 
```bash
npm install
```
Open the remote server:
```bash
npm start
```
Copy and paste the link in the terminal, should be:
`http://localhost:3000`

Play around with the website, seeing the different scores the AI predicts!

## Features

Hoops-Analytics offers a range of features designed to enhance your NBA game analysis:

- **Predictive Modeling**: Utilizes advanced machine learning algorithms to predict game outcomes and player performance metrics.
- **Data Insights**: Dive deep into NBA game statistics to uncover trends and patterns that are not immediately obvious.
- **User-Friendly Interface**: Interact with the analytics through a simple web interface, making complex data more accessible.
- **Customizable Queries**: Users can specify any player from 47 years of data!

## Directory
```bash
├── public                   # Web assets and static files
│   ├── css                  
│   │   └── index.css        # Main stylesheet
│   ├── images               
│   │   └── basketball_court.jpeg 
│   └── index.html           # Entry point HTML file
├── saved_models             # Stores trained model files
│   ├── model_one.pth        
│   └── model_two.pth        
├── src                      
│   ├── config               
│   │   └── sql_setup.py     # SQL database setup script
│   ├── data                 # Scripts to handle data manipulation and loading
│   │   ├── __init__.py      
│   │   ├── convert_data.py  # Converts data formats for model consumption
│   │   ├── fetch_data.py    # Fetches data from external sources or APIs
│   │   └── load_data.py     # Loads data into the application or database
│   ├── model                
│   │   ├── model_one.py     # Defines first machine learning model
│   │   └── model_two.py     # Defines second machine learning model
│   └── scripts             
│       ├── __init__.py      
│       ├── train_model_one.py # Script to train first model
│       ├── train_model_two.py # Script to train second model
│       └── main.py          # Main script to populate database and train model
├── .gitignore               
├── index.js                 # Main JavaScript file for Node.js server
├── LICENSE                  
├── package-lock.json        #
├── package.json             # Node.js manifest file, defines project dependencies
└── simulate.py              # Script called by index.js for custom simulations
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact
For questions or feedback, please reach out to perezlugosantiago@gmail.com.

## Enhanced Documentation**:
nba_api link: `https://github.com/swar/nba_api`




