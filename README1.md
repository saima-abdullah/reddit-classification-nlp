# Understanding Consumer Trends: Classifying Reddit Discussions to Guide Product Innovation
## Problem Statement:
This project aims to help a global technology company understand how online communities are discussing technology innovations and gadgets. By analyzing posts from two key subreddits—r/technology and r/gadgets—we classify discussions into various technology categories, enabling the company to track emerging trends, guide product development, and tailor marketing strategies.\
The primary objective is to build a machine learning model that automatically classifies Reddit posts into technology-related categories, providing actionable insights to help the company stay ahead in the competitive consumer electronics market.
## Background:
Reddit is a social media platform and online community where users share, discuss, and vote on content across a wide range of topics through subreddit forums.\
[r/technology](https://www.reddit.com/r/technology/) is one of the largest subreddits dedicated to discussions about technology. With millions of members, it serves as a hub for tech enthusiasts, professionals, and casual users to share news, insights, and opinions on the latest technological advancements. The subreddit covers a broad range of topics, including emerging technologies such as AI, quantum computing, cybersecurity, 5G, and blockchain. It is widely recognized as a platform where users discuss technology trends, breakthroughs, and innovations that shape industries and everyday life.\
[r/gadgets](https://www.reddit.com/r/gadgets/) is a subreddit dedicated to the latest consumer electronics, devices, and gadgets. With a highly engaged community, r/gadgets focuses on product reviews, recommendations, and discussions about the functionality, usability, and innovations of consumer technology. From smartphones and smartwatches to gaming consoles and wearables, this subreddit is a go-to place for tech-savvy consumers to learn about and discuss the latest gadgets in the market.
## Data Description:
The data used for this project is posts from r/technology and r/gadgets, obtained using the Reddit API.
* [reddit_posts_comments.csv](./data/reddit_posts_comments1.csv): Contains all of the data for our model.


### Size
- **Samples**: 2,930
- **Features**: 6

### Target
- **Type**: Classification
- **Target Variable**: subreddit
- The goal is to predict the subreddit by analyzing the text. We will use Reddit posts scraped from the r/technology and r/gadgets subreddits. The data will include:
### Data Dictionary
Below is a summary of features of the dataset. 


| Feature          | Type     | Dataset             | Description                                                                                   |
|------------------|----------|---------------------|-----------------------------------------------------------------------------------------------|
|post_id              | object    | reddit_posts| A unique identifier for each Reddit post.                                                                           |
| title            | object    | reddit_posts|The title of the Reddit post.
| content     | object    | reddit_posts| The body text or main content of the Reddit post.|
| created_utc       | float  |reddit_posts|The timestamp of when the post was created in UTC.
| subreddit    | object  | reddit_posts|The specific subreddit (e.g., r/technology or r/gadgets) where the post was made.|
|comments       | object    | reddit_posts| The list of user comments associated with the Reddit post.      

### Exploratory Data Analysis (EDA)
Below are some visual insights gathered during the Exploratory Data Analysis phase:

![Distribution of Sale Prices](./img/Distribution_of_Sale_Prices.png)  
*Figure 1: Distribution of Sale Prices showing skewness.*

![Correlation Heatmap](./img/Heatmap_of_correration_between_numeric_features_and_saleprice.png)  
*Figure 2: Heatmap of correlations between numeric features and SalePrice.*

These plots highlight the relationships between key features and the target variable, as well as the overall distribution of the target.



## Model Performance and Evaluation
We tested several regression models to predict housing prices using the Ames dataset without taking into account the neighborhood, aiming to build a more robust model for sale price prediction applicable to any area. Below is a summary of the performance metrics (R-squared Training, R-squared Testing, MSE, RMSE) for each model on both the training and test datasets. The model evaluation was based on cross-validation to ensure robustness and prevent overfitting.

### Summary of Model Performance
| Model               | Training R-squared | Test R-squared |MSE |RMSE | Notes                          |
|---------------------|--------------------|----------------|---------------|-----------|-------------------------------|
| Linear Regression   | 0.82               | 0.83           |0.03        | 0.17   | Baseline model (including only numeric features highly correlated with Sale Price)               |
| Ridge Regression    | 0.81              | 0.82         | 0.03       | 0.17   | Improved with regularization  |
| Lasso Regression    | 0.91             |  0.87       | 0.02     |  0.17 | Feature selection via L1 norm |
| **Final Model: Lasso Regression**   | **0.86**               |**0.88**           | **0.02**     | **0.14**    | Selected for its optimal mix of precision and simplicity without using neighbohood features|

.

## Conclusion
The analysis demonstrates that Lasso Regression is the optimal model for predicting house sale prices without relying on neighborhood data. Its combination of high predictive accuracy, effective feature selection, and interpretability makes it a robust choice. The model performs consistently across training and test datasets, highlighting its reliability and generalizability in different contexts. By focusing on the most relevant features, Lasso Regression simplifies the prediction process while maintaining precision, making it suitable for practical deployment in real estate price prediction tasks.

## Key Takeaways
- **Lasso Regression Performs Best**: Combines high accuracy with simplicity through feature selection, making it ideal for robust predictions.
- **Effective Without Neighborhood Data**: The model reliably predicts sale prices without relying on location-specific factors, enhancing generalizability.
- **Feature Selection is Crucial**: Lasso's ability to focus on key features improves model interpretability and reduces complexity.
- **Consistent Performance**: Strong and consistent results on training and test sets demonstrate reliable, real-world applicability.


## Next Steps
- Broaden the analysis scope by applying the model to different regions or datasets to test its adaptability and performance beyond the original data, enhancing its versatility for broader real estate applications.
- Expand the feature set by including relevant factors like economic indicators, market conditions, or property-specific improvements to enhance model accuracy and robustness.


