/** @format */

import { useState, useEffect } from 'react';
import axios from 'axios';

const useFetch = (apiUrl: string) => {
  const [loading, setLoading] = useState<boolean>(true);
  const [data, setData] = useState([]);
  const [error, setError] = useState<any>();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await axios.get(apiUrl);

        if (!response.data.length) {
          return;
        }
        setData(response.data);
        console.log('response', response.data);
        setLoading(false);
      } catch (error) {
        setError(error);
        setLoading(false);
      }
    };

    fetchData();
  }, [apiUrl, data]);

  return { loading, data, error };
};

export default useFetch;
