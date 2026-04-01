import pandas as pd


class VolatilityRegimeDetector:
    def __init__(self, vol_window: int = 20,
                 low_vol_threshold: float = 0.8,
                 high_vol_threshold: float = 1.2):
        self.vol_window = vol_window
        self.low_vol_threshold = low_vol_threshold
        self.high_vol_threshold = high_vol_threshold

    def detect(self, df: pd.DataFrame) -> dict:
        """
        Detect volatility regime using rolling realized volatility.
        Expected columns: ['close']
        """
        if "close" not in df.columns:
            raise ValueError("DataFrame must contain a 'close' column.")

        if len(df) < self.vol_window + 5:
            return {
                "regime": "unknown",
                "volatility": None,
                "baseline_volatility": None,
                "ratio": None,
                "reason": "not enough data"
            }

        returns = df["close"].pct_change()
        rolling_vol = returns.rolling(self.vol_window).std()
        current_vol = rolling_vol.iloc[-1]
        baseline_vol = rolling_vol.mean()

        if pd.isna(current_vol) or pd.isna(baseline_vol) or baseline_vol == 0:
            return {
                "regime": "unknown",
                "volatility": None,
                "baseline_volatility": None,
                "ratio": None,
                "reason": "invalid volatility calculation"
            }

        ratio = current_vol / baseline_vol

        if ratio < self.low_vol_threshold:
            regime = "low_vol"
        elif ratio > self.high_vol_threshold:
            regime = "high_vol"
        else:
            regime = "normal_vol"

        return {
            "regime": regime,
            "volatility": float(current_vol),
            "baseline_volatility": float(baseline_vol),
            "ratio": float(ratio),
            "reason": f"current/baseline volatility ratio = {ratio:.2f}"
        }
