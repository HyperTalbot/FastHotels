"use client"

import React, { useEffect, useState } from 'react';
import { AppstoreOutlined, 
  MailOutlined, 
  SettingOutlined,  
  EditOutlined, 
  EllipsisOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { Menu, Layout, theme, Carousel, Card, Space, Avatar, Typography, Button } from 'antd';
import axios from 'axios';
import Link from 'next/link';

const { Meta } = Card;

const contentStyle: React.CSSProperties = {
  height: '160px',
  color: '#fff',
  lineHeight: '160px',
  textAlign: 'center',
  background: '#364d79',
};

const { Title } = Typography;

const { Header, Sider, Content } = Layout;


const App: React.FC = async () => {

  return (
    <>
      <Title>Главная страница</Title>

      <Button type="primary" style={{ marginTop: 24 }}>
        <Link href={`/hotels`}>
          Перейти к выбору отелей
        </Link>
      </Button>
    </>
  );
};

export default App;