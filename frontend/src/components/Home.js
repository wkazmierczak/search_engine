import React, { Component } from 'react';
import { Box, Text, Input, Button } from "@chakra-ui/react";

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
        searchResults: [],
        searchTerm: '',
        searchSubmitted: false,
      };
      this.handleSearchChange = this.handleSearchChange.bind(this);
      this.handleSearch = this.handleSearch.bind(this);
    }

    handleSearchChange(event) {
      this.setState({ searchTerm: event.target.value });
    }

    handleSearch() {
      const { searchTerm } = this.state;

      fetch('http://127.0.0.1:5000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: searchTerm.split(' ').filter(word => word.trim() !== '') })
      })
      .then(response => response.json())
      .then(data => {
        this.setState({
          searchResults: data.results,
          searchSubmitted: true,
        });
      })
      
      .catch(error => {
        console.error('Error fetching search results:', error);
      });
    }

  render() {
    const { searchResults, searchSubmitted } = this.state;

    return (
      <Box className="Home">
        <Box height="30vh" display="flex" alignItems="center" justifyContent="center">
          <Text style={{ fontSize: '48px' }}>Search Engine</Text>
        </Box>
        <Box display="flex" alignItems="center" justifyContent="center" mt="4">
          <Input
            placeholder="Enter search term"
            variant="filled"
            value={this.state.searchTerm}
            onChange={this.handleSearchChange}
            onKeyDown={event => {
              if (event.key === 'Enter') {
                this.handleSearch();
              }
            }}
            mr="2"
            width="600px"
            height="20px"
          />
          <Button bg="black" onClick={this.handleSearch} height="25px" color="white">Search</Button>
        </Box>
        {searchSubmitted && (
          <Box mt="4" textAlign="center">
            <Text fontSize="lg">Search Results:</Text>
            <Box mt="2">
              {searchResults.map(result => (
                <Box key={result[1]} mt="2">
                  <p><strong style={{ fontSize: 'larger' }}>{result[2]}</strong></p>
                  <p>Correlation: {result[0]}</p>
                  <p>URL: <a href={result[1]} target="_blank" rel="noopener noreferrer">{result[1]}</a></p>
                  <p>-----------------------</p>
                </Box>
              ))}
            </Box>
          </Box>
        )}
      </Box>
    );
  }
  
}

export default Home;

