import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Product = ({ productId }) => {
  const [product, setProduct] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!productId) return;  // Prevent the API call if no productId is provided

    const fetchProduct = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/product/${productId}`);
        setProduct(response.data);
        setError(null); // Clear any previous errors
      } catch (err) {
        setError("Error occurred while fetching product details!");
        console.error("Error fetching product", err);
      }
    };

    fetchProduct();
  }, [productId]);

  if (error) return <div>{error}</div>;  // Show error message if there is an error
  if (!product) return <div>Loading...</div>;  // Display a loading message until product data is fetched

  // Format the last_checked date to be more readable (optional)
  const lastCheckedDate = new Date(product.last_checked);
  const formattedLastChecked = lastCheckedDate.toLocaleString();  // You can change the format here as needed

  return (
    <div>
      <h2>{product.title}</h2>
      <p>Price: £{product.current_price}</p>
      <p>Last Checked: {formattedLastChecked}</p> {/* Display the formatted last_checked */}
    </div>
  );
};

export default Product;
