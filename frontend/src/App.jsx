import { AppProvider } from "./context/AppContext";
import Header from "./components/layout/Header";
import Sidebar from "./components/layout/Sidebar";
import MainContent from "./components/layout/MainContent";
import "./styles/variables.css";
import "./styles/global.css";

export default function App() {
  return (
    <AppProvider>
      <div className="app-layout">
        <Header />
        <Sidebar />
        <MainContent />
      </div>
    </AppProvider>
  );
}
