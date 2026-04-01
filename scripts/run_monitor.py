import pandas as pd
from src.regime.volatility_regime import VolatilityRegimeDetector


def load_sample_data():
    data = {
        "close": [
            100, 101, 100.5, 101.2, 101.8, 102.4, 102.0, 101.7, 102.9, 103.2,
            102.8, 103.5, 104.0, 103.6, 104.5, 105.2, 104.8, 105.6, 106.1, 105.4,
            106.8, 107.5, 106.9, 108.0, 109.2, 108.8, 110.5, 109.6, 111.4, 110.9
        ]
    }
    return pd.DataFrame(data)


def main():
    df = load_sample_data()
    detector = VolatilityRegimeDetector(vol_window=5)
    result = detector.detect(df)

    print("Volatility Regime Report")
    print("------------------------")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
