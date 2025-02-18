import React, { useState } from "react";
import './App.css';
import Product from './components/Product'; // Import the Product component

const App = () => {
  const [urls, setUrls] = useState("");
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Handle the form submission to send URLs to the backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    const urlList = urls.split("\n").map(url => url.trim()).filter(url => url.length > 0);

    setLoading(true); // Set loading to true when starting the fetch
    setError(null); // Reset previous errors

    try {
      const response = await fetch("http://localhost:8000/scrape-products", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ urls: urlList }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch products");
      }

      const data = await response.json();
      setProducts(data.products);
    } catch (err) {
      setError("Error occurred while scraping products.");
      console.error(err);
    } finally {
      setLoading(false); // Set loading to false after the operation is done
    }
  };

  return (
    <div className="App">
      <h1>Scrape Products</h1>

      {/* Form to input multiple URLs */}
      <form onSubmit={handleSubmit}>
        <textarea
          value={urls}
          onChange={(e) => setUrls(e.target.value)}
          rows="6"
          cols="40"
          placeholder="Enter product URLs, one per line"
        ></textarea>
        <br />
        <button type="submit" disabled={loading}>Scrape Products</button>
      </form>

      {error && <p className="error">{error}</p>} {/* Display error if any */}

      {loading ? (
        <p>Loading...</p>
      ) : (
        <div>
          {products.length > 0 && (
            <ul className="product-list">
              {products.map((product) => {
                const lastCheckedDate = new Date(product.last_checked);
                const formattedLastChecked = lastCheckedDate.toLocaleString();

                return (
                  <li key={product.id} className="product-item">
                    <Product productId={product.id} /> {/* Display product details */}
                    <p>Last Checked: {formattedLastChecked}</p> {/* Display last_checked */}
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default App;
