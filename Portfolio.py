import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Step 1: Historical Market Data
def load_market_data():
    # Simulate historical data for simplicity
    # In a real project, replace this with actual data (e.g., from Yahoo Finance or FRED)
    data = {
        'Date': pd.date_range(start='2000-01-01', periods=252 * 20, freq='B'),
        'Stocks': np.random.normal(0.0003, 0.02, 252 * 20).cumsum(),
        'Bonds': np.random.normal(0.0001, 0.01, 252 * 20).cumsum(),
        'RealEstate': np.random.normal(0.0002, 0.015, 252 * 20).cumsum(),
    }
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)
    return df

# Step 2: Apply Stress Scenario
def apply_stress_scenario(portfolio, scenario):
    stressed_portfolio = portfolio.copy()
    for asset, change in scenario.items():
        if asset in stressed_portfolio.columns:
            stressed_portfolio[asset] *= (1 + change)
    return stressed_portfolio

# Step 3: Simulate Portfolio Performance
def simulate_portfolio(portfolio_weights, market_data):
    returns = market_data.pct_change().dropna()
    portfolio_returns = returns.dot(portfolio_weights)
    portfolio_cum_returns = (1 + portfolio_returns).cumprod()
    return portfolio_cum_returns

# Step 4: Visualization
def plot_performance(portfolio_returns, title):
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_returns.index, portfolio_returns, label='Portfolio Performance')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Step 5: Streamlit App
def main():
    st.title("Portfolio Stress Tester")

    # Sidebar for portfolio inputs
    st.sidebar.header("Portfolio Allocation")
    stocks_weight = st.sidebar.slider("Stocks (%)", 0, 100, 60)
    bonds_weight = st.sidebar.slider("Bonds (%)", 0, 100, 30)
    real_estate_weight = st.sidebar.slider("Real Estate (%)", 0, 100, 10)

    if stocks_weight + bonds_weight + real_estate_weight != 100:
        st.sidebar.error("Portfolio weights must sum to 100%")
        return

    portfolio_weights = {
        'Stocks': stocks_weight / 100,
        'Bonds': bonds_weight / 100,
        'RealEstate': real_estate_weight / 100,
    }

    # Load historical market data
    market_data = load_market_data()
    st.write("### Historical Market Data")
    st.dataframe(market_data.head())

    # Simulate portfolio performance
    portfolio_returns = simulate_portfolio(
        pd.Series(portfolio_weights), market_data
    )
    st.write("### Portfolio Performance")
    plot_performance(portfolio_returns, "Baseline Portfolio Performance")

    # Stress Scenarios
    st.sidebar.header("Stress Scenarios")
    scenario = {
        'Stocks': st.sidebar.slider("Stocks Impact (%)", -100, 100, -30) / 100,
        'Bonds': st.sidebar.slider("Bonds Impact (%)", -100, 100, -10) / 100,
        'RealEstate': st.sidebar.slider("Real Estate Impact (%)", -100, 100, -20) / 100,
    }

    # Apply stress scenario
    stressed_market_data = apply_stress_scenario(market_data, scenario)
    stressed_portfolio_returns = simulate_portfolio(
        pd.Series(portfolio_weights), stressed_market_data
    )
    st.write("### Stressed Portfolio Performance")
    plot_performance(stressed_portfolio_returns, "Stressed Portfolio Performance")

    # Insights
    baseline_final_value = portfolio_returns.iloc[-1]
    stressed_final_value = stressed_portfolio_returns.iloc[-1]
    st.write(f"Baseline Portfolio Final Value: {baseline_final_value:.2f}")
    st.write(f"Stressed Portfolio Final Value: {stressed_final_value:.2f}")
    st.write(
        f"Portfolio Loss Under Stress: {(baseline_final_value - stressed_final_value) / baseline_final_value:.2%}"
    )

if __name__ == "__main__":
    main()
