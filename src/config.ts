interface Config {
  API_URL: string;
}

const development: Config = {
  API_URL: 'http://localhost:8000',
};

const production: Config = {
  API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
};

export const config: Config = 
  import.meta.env.PROD ? production : development;