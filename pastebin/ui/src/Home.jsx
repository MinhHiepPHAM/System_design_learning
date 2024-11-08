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


import axios from 'axios';

function Home() {
    const [paste, setPaste] = useState('');
    const [expiration, setExpiration] = useState(0);
    const [shortlink, setShortlink] = useState('');
    const [linkInfos, setLinkInfos] = useState([]);

    useEffect(() => {
        async function fetchData() {
            const response = await axios.get('/', {headers:headers});
            setLinkInfos(
                response.data.map(item => (
                    {'link': item.shortlink, 'created': item.created_at, 'size': item.size}
                ))
            ) 
        }

        fetchData();

    },[shortlink]);

    const displayLinks = 
    <Flex direction='column' mt='xl'>{
        linkInfos.map((info,i) => (
            <a href={`/detail/${info.link}`} key={i}>{info.link}, created at {info.created}, size={info.size}</a>
    ))}
    </Flex>;

    const headers = {'Content-Type': 'application/json'};

    const handleSubmitButton = async (e) => {
        const response = await axios.post(`/create/`, {
            paste,
            expiration
        }, {headers:headers});

        setShortlink(response.data.shortlink);
        // console.log('Response:', response)

    }

    const copyButton =  (
        <Flex direction='row'>
            <CopyButton value={shortlink}>
            {
                ({copied, copy}) => (
                    <Button ml='xl' mr='xs' fw='normal' variant='outline' onClick={copy}>
                        {copied ? 'Copied': 'Copy url'}
                    </Button>
                )
            }
            </CopyButton>
            <TextInput w={250} value={shortlink} onChange={(e)=>{}}/>
        </Flex>
    );
    

    return( 
    <>
        <a href='/'><Title c='blue' order={2}>Pastebin</Title></a>
        <Textarea
            label='New paste' required
            placeholder='Type the context you want to paste'
            mt='xl' mr='xl'
            autosize
            minRows={6}
            onChange={(e)=>setPaste(e.currentTarget.value)}
        />
        <Flex direction='row' align='flex-end'>
            <NumberInput
                label='Expiration' required
                placeholder='Expired in minutes'
                min={0}
                mt='md' maw={200} mr='xl'
                onChange={setExpiration}
            />
            <Button variant='outline'
                fw='normal'
                onClick={handleSubmitButton}
            >Submit</Button>
            {shortlink && copyButton}
        </Flex>
        <div align='left'>
            {displayLinks}
        </div>
    </>
    )
}

export default Home;
