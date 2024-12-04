import React, { useState } from 'react';

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');

  const handleSearch = () => {
    onSearch(query); // Fonction à appeler pour traiter la recherche
    setQuery(''); // Réinitialiser le champ
  };

  return (
    <div className="searchBar">
      <input
        type="text"
        placeholder="Ask Anything..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
}

export default SearchBar;
