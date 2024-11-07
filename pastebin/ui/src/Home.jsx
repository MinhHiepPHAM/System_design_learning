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

    const links = [
        {'link': 'aaaaaaab', 'created':'1 min ago', 'size':'15KB'},
        {'link': 'aaaa5Dab', 'created':'2 min ago', 'size':'07KB'},
        {'link': 'aaaa12ab', 'created':'5 min ago', 'size':'10KB'},
    ]

    const linkInfos = (<List mt='xl'>{
        links.map((info,i) => (
            <List.Item key={i}>{info.link} created at {info.created} with size={info.size}</List.Item>
        ))        
    }</List>);



    const handleSubmitButton = async (e) => {
        const headers = {'Content-Type': 'application/json'};
        
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
    
    // console.log('paste:', paste, expiration)

    return( 
    <>
        <Title c='blue' order={2}>Pastebin</Title>
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
            {linkInfos}
        </div>
    </>
    )
}

export default Home;
