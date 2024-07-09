# Hoops-Analytics

<img width="1469" alt="Screenshot 2024-07-08 at 7 54 00 PM" src="https://github.com/santiagoperezlugo/Hoops-Analytics/assets/144164736/c8b66fd4-efbf-4990-b2c4-ad0c30ae5c47">

## Introduction
Hoops-Analytics harnesses the power of deep learning to succesfully predict 66% of over 50,000 NBA games correctly, and with an average distance of 8 points from the true score. Built using PyTorch, this platform uses a neural network model which features layers of linear transformations, ReLU activations, batch normalization, and dropout to mitigate overfitting. This allows the model to learn complex patterns and dependencies in 47 years of NBA data, optimizing predictions through an Adam optimizer and SmoothL1Loss for refined accuracy.

## Prerequisites
- Python 3.8+
- MySQL Server
- Python libraries: `mysql.connector`, `pandas`, `numpy`, `nba_api`

### Installation

a . git clone <repository-url>

b. `pip3 install -r requirements.txt`

### Set Environment Variables in Your Session:
```bash
export DB_HOST='127.0.0.1'

export DB_USER="root"

export DB_PASSWORD="your_password"

export DB_NAME="nba_data"
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

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact
For questions or feedback, please reach out to perezlugosantiago@gmail.com.

## Enhanced Documentation**:
nba_api link: `https://github.com/swar/nba_api`




