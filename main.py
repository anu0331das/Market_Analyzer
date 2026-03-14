from market_engine import MarketAnalyzer

def start_pipeline():
    print("--- Starting Market Analysis Pipeline ---")
    
    # Define your instruments (ES and NQ futures)
    # Using =F because that is how Yahoo Finance labels futures
    assets = [
        MarketAnalyzer("ES=F", "ES_Emini"),
        MarketAnalyzer("NQ=F", "NQ_Emini")
    ]

    for asset in assets:
        print(f"[*] Processing {asset.name}...")
        
        # 1. Fetch data from API
        asset.fetch_market_data()
        
        # 2. Run statistical math
        vol = asset.compute_indicators()
        
        # 3. Save the visual report
        report_file = asset.plot_and_save(vol)
        
        print(f"[+] Success: {asset.name} Volatility is {vol:.2%}")
        print(f"[+] Report saved: {report_file}\n")

    print("--- ✅ All tasks complete. Check your folder for images! ---")

if __name__ == "__main__":
    start_pipeline()