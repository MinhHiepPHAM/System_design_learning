import {
    Box,
    Flex,
    Textarea,
    NumberInput,
    List,
    Grid
} from '@mantine/core';

import axios from 'axios';

function Home() {

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
        

    return( 
    <>
        <Textarea
            label='New paste' required
            placeholder='Type the context you want to paste'
            mt='xl' mr='xl'
            autosize
            minRows={6}
            
        />
        <NumberInput
            label='Expiration' required
            placeholder='Expired in minutes'
            min={0}
            mt='md' maw={200}
        />
        <div align='left'>
            {linkInfos}
        </div>
    </>
    )
}

export default Home;
