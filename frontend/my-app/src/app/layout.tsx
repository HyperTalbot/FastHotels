import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Footer, Header } from "antd/es/layout/layout";
import { BellFilled, BellTwoTone, HeartFilled, HeartTwoTone, } from '@ant-design/icons';
import { Avatar, Badge, Space } from "antd";
// import { headerStyle, footerStyle } from "@/app/consts"

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

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
  padding: '50px'
};

export const metadata: Metadata = {
  title: "FastHotels",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        <header>
          <>
            <Header style={headerStyle}>
              Быстрые Отели! 
              <HeartFilled />  
              <BellFilled />
              {/* <HeartTwoTone /> */}
              {/* <Space size={24}>
                <Badge count={1}> 
                  <Avatar shape="square" icon={""} />
                </Badge>
              </Space> */}
            </Header>
          </>
        </header>
        <main>
          {children}
        </main>
        <footer><Footer style={footerStyle}>
          Безопасность платежей <br /> Надёжная защита данных от ведущих платёжных систем.
        </Footer></footer>
      </body>
    </html>
  );
}
