import React, { useState } from "react";
import "./styles.css";
import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";

const Home = () => {
  const [searchValue, setSearchValue] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSearchCompleted, setIsSearchCompleted] = useState(false);

  const handleSearch = async () => {
    try {
      setIsLoading(true); // 设置为正在加载状态
      const response = await fetch("http://localhost:5000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: searchValue }), // 将搜索词作为请求体发送给后端
      });
      if (!response.ok) {
        throw new Error("Request failed");
      }
      const results = await response.json(); // 解析返回的JSON结果
      setSearchResults(results); // 更新搜索结果状态
      setIsLoading(false); // 设置为加载完成状态
      setIsSearchCompleted(true); // 设置搜索完成状态
    } catch (error) {
      console.log("Error:", error);
      setIsLoading(false); // 设置为加载完成状态
      setIsSearchCompleted(true); // 设置搜索完成状态
    }
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
        <IconButton
          type="button"
          sx={{ p: "10px" }}
          aria-label="search"
          className="mg"
          onClick={handleSearch}
        >
          <SearchIcon />
        </IconButton>
        <input
          type="text"
          id="search"
          value={searchValue}
          placeholder="Search the information you want or type a URL"
          onChange={(e) => setSearchValue(e.target.value)}
          onKeyDown={handleKeyDown}
          autoComplete="off"
          name="keyword"
          style={{
            fontSize: "16px",
            fontFamily: "Roboto",
            letterSpacing: "0.25px",
          }}
        />
      </div>
      {isLoading && <div className="no-results">Loading...</div>}
      {!isLoading && searchResults.length === 0 && isSearchCompleted && (
        <div className="no-results">
          Sorry, we could not find the relevant articles for your query...
        </div>
      )}
      {!isLoading && searchResults.length > 0 && (
        <div className="results">{renderSearchResults()}</div>
      )}
    </div>
  );
};

export default Home;
