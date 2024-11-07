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
} from '@mantine/core';

import { useEffect, useState } from 'react';
import  {useParams} from 'react-router-dom';

import axios from 'axios';

function ShortLink() {
    const [context, setContext] = useState('')
    const [expiration, setExpiration] = useState('')
    const [size, setSize] = useState('')

    const {shortlink} = useParams();
    async function fetchData() {
        const response = await axios.get(`/detail/${shortlink}`)
        setExpiration(response.data.expiration)
        setContext(response.data.context)
        setSize(response.data.size)
    }

    fetchData();
    
    return (
    <>
        <a href='/'><Title c='blue' order={2}>Pastebin</Title></a>
        <Textarea
            label={`Paste (${size}) will be expired at ${expiration}`}
            value={context}
            mt='xl'
            autosize
            minRows={6}
            onChange={(e)=>{}}
        />
        <CopyButton value={context}>
        {
            ({copied, copy}) => (
                <Button mt='md' fw='normal' variant='outline' onClick={copy}>
                    {copied ? 'Copied': 'Copy context'}
                </Button>
            )
        }
        </CopyButton>


    </>
    )


}

export default ShortLink;
