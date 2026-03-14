import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class MarketAnalyzer:
    """
    Professional-grade engine for fetching and analyzing Futures data.
    Demonstrates OOP, API integration, and statistical modeling.
    """
    
    def __init__(self, ticker, name):
        self.ticker = ticker
        self.name = name
        self.data = None

    def fetch_market_data(self, period="1y"):
        """Pull data from Yahoo Finance API with error handling."""
        try:
            # Use =F for futures (ES=F, NQ=F)
            self.data = yf.download(self.ticker, period=period)
            if self.data.empty:
                raise ValueError(f"No data found for {self.ticker}.")
        except Exception as e:
            print(f"[!] API Error for {self.ticker}: {e}")

    def compute_indicators(self):
        """Vectorized calculations for SMAs and Annualized Volatility."""
        # Calculate 20 and 50 Day Moving Averages
        self.data['SMA_20'] = self.data['Close'].rolling(window=20).mean()
        self.data['SMA_50'] = self.data['Close'].rolling(window=50).mean()
        
        # Calculate Daily Log Returns
        self.data['Returns'] = np.log(self.data['Close'] / self.data['Close'].shift(1))
        
        # Annualize the Volatility (Standard Deviation * sqrt of trading days)
        vol = self.data['Returns'].std() * np.sqrt(252)
        return vol

    def plot_and_save(self, annualized_vol):
        """Generate a high-fidelity Seaborn dashboard saved to disk."""
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(12, 6))
        
        # Plotting Price and Moving Averages
        plt.plot(self.data['Close'], label='Price', color='black', alpha=0.4)
        plt.plot(self.data['SMA_20'], label='20-Day SMA', color='#0077b6', lw=1.5)
        plt.plot(self.data['SMA_50'], label='50-Day SMA', color='#e63946', lw=1.5)
        
        plt.title(f"{self.name} Analysis | Annualized Vol: {annualized_vol:.2%}", fontsize=14)
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.legend(loc='best')
        
        # Save as a professional PNG file
        filename = f"{self.name.lower()}_report.png"
        plt.savefig(filename, dpi=300)
        plt.close() # Closes the plot so it doesn't stay in memory
        return filename