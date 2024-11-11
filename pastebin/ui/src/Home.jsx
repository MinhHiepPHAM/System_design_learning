import {
    Flex,
    Textarea,
    NumberInput,
    List,
    Button,
    CopyButton,
    TextInput,
    Title,
    Text,
} from '@mantine/core';

import { useEffect, useState } from 'react';
import { useNavigate } from "react-router-dom";

import axios from 'axios';

function Home() {
    const [paste, setPaste] = useState('');
    const [expiration, setExpiration] = useState(0);
    const [shortlink, setShortlink] = useState('');
    const [linkInfos, setLinkInfos] = useState([]);
    const [query, setQuery] = useState("");
    const navigate = useNavigate()

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
    <Flex direction='column' mt='md'>{
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
        <Flex direction='row' mt='xl'>
            <TextInput
                placeholder='Search created pastes'
                onChange={(e)=>setQuery(e.currentTarget.value)}
            />
            <Button
                fw='normal' ml='xs'
                variant='outline'
                onClick={(e)=> {navigate(`/search/${query}`)}}
            >Search</Button>
        </Flex>
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
            <Flex direction='row' mt='xl'>
                <Text size='lg' fw={500} c='blue' mr='xl'>Recent pastes</Text>
                <a href={'/all'} style={{textDecoration: 'underline'}}>View all</a>
            </Flex>
            {displayLinks}
        </div>
    </>
    )
}

export default Home;
