import { useEffect } from "react"

const TradingWidget = () => {
  useEffect(() => {
    const script = document.createElement("script")
    script.src = "https://s3.tradingview.com/external-embedding/embed-widget-market-overview.js"
    script.async = true
    script.innerHTML = JSON.stringify({
      colorTheme: "dark",
      dateRange: "12M",
      showChart: true,
      locale: "en",
      width: "100%",
      height: "400",
      largeChartUrl: "",
      isTransparent: false,
      showSymbolLogo: true,
      showFloatingTooltip: false,
      symbolsGroups: [
        {
          name: "主要市場",
          originalName: "Indices",
          symbols: [
            { name: "OANDA:SPX500USD", displayName: "S&P 500" },
            { name: "OANDA:NAS100USD", displayName: "NASDAQ 100" },
            { name: "FOREXCOM:DJI", displayName: "Dow Jones" }
          ]
        }
      ]
    })
    document.getElementById("tradingview-widget")?.appendChild(script)
  }, [])

  return <div id="tradingview-widget" style={{ width: "100%", height: "400px" }} />
}

export default TradingWidget