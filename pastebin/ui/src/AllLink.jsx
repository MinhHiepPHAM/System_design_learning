import {
    Title,
    Pagination,
    Flex
} from '@mantine/core';

import { useEffect, useState } from 'react';
import  {useParams} from 'react-router-dom';

import axios from 'axios';

function AllLink() {
    const [linkInfo, setLinkInfo] = useState([]);
    const [pageNum, setPageNum] = useState(1);
    const [total, setTotal] = useState(1)

    const headers = {'Content-Type': 'application/json'};
    useEffect(()=>{
        async function fetchData() {
            const response = await axios.get(`/all?page=${pageNum}`, {headers: headers});
            
            setLinkInfo(
                response.data.link_infos.map(item => (
                    {'link': item.shortlink, 'created': item.created_at, 'size': item.size}
                ))
            );
            setTotal(response.data.num_page);
        }
        fetchData();

    },[pageNum]);

    

    const allLinks = (
    <Flex direction='column' ml='lg'>
    {
        linkInfo.map((info,i)=>(
        <a href={`/detail/${info.link}`} key={i}>{info.link}, created at {info.created}, size={info.size}</a>
    ))}
    </Flex>
    );
    
    return (
    <>
        <a href='/'><Title c='blue' order={2}>Pastebin</Title></a>
        <Title mt='xl' mb='lg' order={3} c='blue.5'>All pastes</Title>
        {allLinks}
        <Pagination mt='lg' total={total} siblings={1} defaultValue={1} onChange={setPageNum}/>
    </>
    );
}

export default AllLink;
