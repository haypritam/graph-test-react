import logo from './logo.svg';
import './App.css';
import Graphview from './components/graph';
import WorldCup from './components/worldcup';
import Cite from './components/cite';
import DenseTable from './components/table';
import BasicMenu from './components/menu';

function App() {

  return (
    <div className="App">
      {/* <WorldCup/> */}
      {/* <Graphview/> */}
      <Cite/>
      {/* <DenseTable/> */}
      {/* <BasicMenu items={items}></BasicMenu> */}
    </div>
  );
}

export default App;
