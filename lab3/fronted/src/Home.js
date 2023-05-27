import React, { useState } from "react";
import "./styles.css";
import Searchpng from "./images/search.png";

const Home = () => {
  const [searchValue, setSearchValue] = useState("");
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = () => {
    console.log("Search query:", searchValue);
    setTimeout(() => {
      const results = [
        {
          title:
            "There's a shortage of truckers, but TuSimple thinks it has a solution: no driver needed - CNN",
          summary:
            "The e-commerce boom has exacerbated a global truck driver shortage, but could autonomous trucks help fix the problem?",
          matchRate: "90%",
          url: "https://www.cnn.com/2021/07/14/world/tusimple-autonomous-truck-spc-intl/index.html",
        },
        {
          title: "Result 2",
          summary:
            'Hide Caption 5 of 8 Photos: The robots running our warehousesAlthough not specifically designed for warehouses, Boston Dynamics\' dog-like robot "Spot" can lift objects, pick itself up after a fall, open and walk through doors, and even remind people to practice social distancing.',
          matchRate: "85%",
          url: "https://example.com/result2",
        },
        {
          title: "Result 3",
          summary: "Summary of result 3",
          matchRate: "80%",
          url: "https://example.com/result3",
        },
      ];
      setSearchResults(results);
    }, 10);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  const renderSearchResults = () => {
    return searchResults.map((result, index) => (
      <a
        key={index}
        href={result.url}
        target="_blank"
        rel="noopener noreferrer"
        className="result-card"
      >
        <div className="result-title">{result.title}</div>
        <div className="result-summary-container">
          <span className="summary-label">Summary:</span>
          <span className="result-summary">{result.summary}</span>
        </div>
        <div className="result-match-rate">Match Rate: {result.matchRate}</div>
      </a>
    ));
  };

  return (
    <div className="container">
      <div className="system-name">Information Retrieval System</div>
      <div className="searchbar">
        <img src={Searchpng} className="mg" onClick={handleSearch} />
        <input
          type="text"
          id="search"
          value={searchValue}
          placeholder="Search the information you want or type a URL"
          onChange={(e) => setSearchValue(e.target.value)}
          onKeyDown={handleKeyDown}
          name="keyword"
        />
      </div>
      {searchResults.length > 0 && (
        <div className="results">{renderSearchResults()}</div>
      )}
    </div>
  );
};

export default Home;
