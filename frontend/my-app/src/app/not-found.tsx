import React from 'react';
import { Button, Result } from 'antd';

const App: React.FC = () => (
  <Result
    status="404"
    title="Ошибка: 404"
    subTitle="Страница не найдена."
    extra={<Button type="primary">Вернуться домой</Button>}
  />
);

export default App;
