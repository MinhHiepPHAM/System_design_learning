import './App.css'
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import Home from './Home'
import ShortLink from './ShortLink'
import AllLink from './AllLink'
import AllSearchResults from './Search'
import {DEFAULT_THEME, MantineProvider, createTheme, mergeThemeOverrides } from '@mantine/core';

// Import styles of packages that you've installed.
// All packages except `@mantine/hooks` require styles imports
import '@mantine/core/styles.css';


const themeOverride = createTheme({
	autoContrast : true,
	luminanceThreshold: 0.66,
	focusRing: 'auto',
	defaultRadius:'sm',
	cursorType: 'pointer',
	primaryShade:6
})
const myTheme = mergeThemeOverrides(DEFAULT_THEME, themeOverride);



function App() {
  return <MantineProvider theme={myTheme}>
            <BrowserRouter>
				<div className="App">	
					<main>
						<Routes>
							<Route path="/" element={<Home/>} />
                            <Route path="/detail/:shortlink" element={<ShortLink/>} />
                            <Route path="/all" element={<AllLink/>} />
                            <Route path="/search/:query" element={<AllSearchResults/>} />
						</Routes>
					</main>
				</div>
			</BrowserRouter>
        </MantineProvider>;
    }

export default App
