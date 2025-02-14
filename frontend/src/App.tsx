import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Provider } from "./providers/ChakraProvider";  // 確保這裡是你剛剛的 Provider.tsx
import Home from "./pages/Home";

function App() {
  return (
    <Provider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </Router>
    </Provider>
  );
}

export default App;