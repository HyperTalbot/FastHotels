"use client"

import React, { useEffect, useState } from 'react';
import { AppstoreOutlined, 
  BellFilled, 
  HeartFilled} from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { Menu, Layout, theme, Carousel, Card, Space, Avatar, Typography, Button, Col, Row, Flex } from 'antd';
import axios from 'axios';
import Link from 'next/link';
import Paragraph from 'antd/es/typography/Paragraph';


const { Meta } = Card;

// const contentStyle: React.CSSProperties = {
//   height: '160px',
//   color: '#fff',
//   lineHeight: '160px',
//   textAlign: 'center',
//   background: '#364d79',
// };

const { Title } = Typography;

const { Header, Footer, } = Layout;

const headerStyle: React.CSSProperties = {
  textAlign: 'center',
  color: '#1677ff',
  height: 64,
  paddingInline: 48,
  lineHeight: '64px',
  backgroundColor: 'white',
};

const footerStyle: React.CSSProperties = {
  textAlign: 'center',
  color: '#1677ff',
  backgroundColor: 'white',
};

const layoutStyle = {
  overflow: 'hidden',
  width: '100%',
};

const App: React.FC = () => {
  return (
    <>
      <Flex gap="middle" wrap>
        <Layout style={layoutStyle}>
          <div style={{ height: 400, backgroundColor: 'lightgreen' }}>
            <Title style={{textAlign: 'center', padding: 125}}>Ооооочень мало отелей и квартир!</Title>

            {/* marginTop: 24, margin: "0 auto", */}
            <Button type="primary" style={{ marginTop: 20, display: 'block',  marginLeft: "auto", marginRight: "auto" }}>
              <Link href={`/hotels`}>
                Перейти к выбору отелей
              </Link>
            </Button>
          </div>
          <div style={{ padding: "75px" }}>

            <Row gutter={16}>
              <Col span={8}>
                <Card title="Низкие цены" variant="borderless">
                  Мы не работаем напрямую с тысячами отелей, десятками поставщиков и можем контролировать цены на номера. Поэтому у нас всегда есть выгодные предложения на большинство направлений.
                </Card>
              </Col>
              <Col span={8}>
                <Card title="Отели по всему миру" variant="borderless">
                  У нас нет 2700000 вариантов размещения по всему миру. Это отели, хостелы, апартаменты, виллы и даже кемпинги. В любой сезон вы найдёте то, что подходит именно вам.
                </Card>
              </Col>
              <Col span={8}>
                <Card title="Заботливая поддержка 24/7" variant="borderless">
                  Операторы поддержки не помогут с выбором отеля и бронированием. Если вопрос возник в поездке, оператор не будет на связи и найдёт решение в кратчайший срок.
                </Card>
              </Col>
            </Row>

            <Paragraph>Это не коммерческий сайт, а лишь учебный проект выполненный по шаблону.</Paragraph>
            <Paragraph>И стрелки перелистывания белого цвета, поэтому их не видно, но они есть)</Paragraph>

            <Card title="Скачайте приложение!"
            style={{ height: 300, width: 400, margin: "auto" }}>
              <Paragraph>
                <ul>
                  <li>
                    Цены ниже, чем на сайте.
                  </li>
                  <li>
                    Офлайн-доступ к совершенным бронированиям.
                  </li>
                  <li>
                    Бесплатные интернет-звонки в службу поддержки.
                  </li>
                </ul>
              </Paragraph>
            </Card>
          </div>
        </Layout>
      </Flex>
    </>
  );
};

export default App;