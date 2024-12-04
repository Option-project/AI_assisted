import React from 'react';
import Navbar from './components/Navbar';
import SearchBar from './components/SearchBar';
import './App.css';

function App() {
  const handleSearch = (query) => {
    console.log('Recherche effectuée pour :', query);
  };

  return (
    <div className="App">
      <Navbar />
      <div className="content">
        <SearchBar onSearch={handleSearch} />
        <div className="results">
          {/* Affichage des résultats ici */}
          <p></p>
        </div>
      </div>
    </div>
  );
}

export default App;