# Efficient_Frontier
Efficient Frontier portfolio optimisation on 4 out of TOP10 NASDAQ companies
In first part of the code we need to download required packages and subpackages: numpy, pandas, matplotlib pandas_datareader.
First step is to download historical prices of NASDAQ TOP 10 companies. For that i created a dictionary which would map Companies names with its market symbols.
Then I downloaded the data from Yahho finance using pandas_dataread and put it into the DataFrame.
In next few lines of the code, I'm just preparing the data for futher analysis - setting up the index, selecting the close prices and sorting teh DataFrame.
Now we can plot the daily prices changes, just to visualize how prices of the stocks changed over that period. I also calculated and plotted the daily percentage returns.
To compare the performance of our 10 Companies we need to download the index prices. This time I'm using the data prepared in the csv file and I'm also creating a DataFrame by using read_csv from pandas package.
Next steps are again - just clearing and preparing the data for further analysis.
Now we can join both DataFrames and calculate the relative performance of the NASDAQ top 10 companies stocks.

PORTFOLIO OPTIMISASTION
In next part of the code I'm selecting 4 companies to crate my portfolio with - Apple, Amazon, Google and Pepsi.
Next step is to calculate the required data for the analysis which are - correlation and covariance of the portfolio, to see how much correlated our companies are. (it's good to have more diversified portfolio, becuse it's more safe).
The main goal of the portfolio optimisation is to find specific weights for each company stocs in the portfolio, so that for given risk level the return are the highest possible. In order to do that, I simulated 1000 portfolios, whith 1000 differnet weight proportions, given risk and the retusns. The resulst of the simulation will be stored in empty lists that I created before the for loop (simulation).
After the simulation, I created a DataFrame which stores 1000 portfolios in order to then show them all on the graph.
To show the results of the simulation I used the scatter plot, which in this case it's easier to read. We can see that the dots created a line which is called a efficiet frontier line. All portfolios that lay on this line are having the highest returns for given risk.
The next step is to find out, where is the most efficient portfolio on this line. For this purpose I used the Max Sharp ratio ans stored this portfolio in maxSharp variable. 
It occures that if we want to build our portfolio with these companies (Apple, Amazon, Google and Pepsi), almost 68% of our portfolio should be allocated in Amazon stocks and the Google stock should be only 0,3%. Our portfolio would give us 0,38 of the retrun with given risk of 0,27.
The last step is to locate our maxSharpe portfolio among other 999 portfolios by plotting it on the scatter plot. I indicated our portfolio with red star.
