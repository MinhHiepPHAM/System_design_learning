import {
    Box,
    Flex,
    Textarea,
    NumberInput,
    List,
    Grid,
    Button,
    CopyButton,
    TextInput,
    Title,
    Loader,
} from '@mantine/core';

import { useEffect, useState } from 'react';
import  {useParams} from 'react-router-dom';

import axios from 'axios';

function SearchResult({context, shortlink, createdat}) {
    return (
    <>
        <a href={`/detail/${shortlink}`}>Paste {shortlink}, created at {createdat}</a>
        <Textarea
            value={context}
            mb='lg'
            autosize
            maxRows={4}
            onChange={(e)=>{}}
        />
    </>
    );

}

function AllSearchResults() {
    const {query} = useParams()
    const [results, setResults] = useState([]);
    const [loaded, setLoaded] = useState(false);

    const headers = {'Content-Type': 'application/json'}
    
    useEffect(()=>{
        async function fetchData() {
        const response = await axios.get(`/search/${query}`, {headers: headers})
        setResults(response.data.results)
    }
    fetchData();
    
    },[loaded]);

    if (results.length == 0) return <Loader color="blue" />;
    
    const allResults = results.map((result, i) => (
        <SearchResult key={i}
            context={result.context} shortlink={result.shortlink} createdat={result.created_at}
        />
    ));

    console.log(results[0].context)

    return (
    <>
        <a href='/'><Title c='blue' order={2}>Pastebin</Title></a>
        <Title c='blue.5' order={4} mb='xl' mt='xl'>Search query: {query} </Title>
        {allResults}
    </>
    );
    
}

export default AllSearchResults;
