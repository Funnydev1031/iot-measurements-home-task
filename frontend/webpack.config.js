const path = require('path');
const { DefinePlugin } = require('webpack');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
// const { WebpackManifestPlugin } = require('webpack-manifest-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = ({target = "client", mode = "development", inputFolder = 'src', outputFolder = 'build'}) => {
    console.log(`Creating webpack config for: ${JSON.stringify({target, mode, inputFolder, outputFolder})}\n`)
    return {
        name: target,
        mode,
        entry: path.resolve(__dirname, inputFolder, 'index.tsx'),
        output: {
            path: path.resolve(__dirname, `${outputFolder}`),
            filename: `${target}/[name].js`,
            publicPath: '/',
        },
        resolve: {
            extensions: ['.ts', '.tsx', '.js', '.json'],
        },
        target: (
            target === 'client' ? 
            'web' :
            target === 'server' ?
            'node' : 
            undefined
        ),
        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    include: path.resolve(__dirname, 'src'),
                    use: {
                        loader: 'babel-loader',
                        options: {
                            presets: ['@babel/preset-env'],
                        },
                    },
                },
            ],
        },
        optimization: {
            splitChunks: {
                chunks: 'all',
                cacheGroups: {
                    vendor: {
                        test: /[\\/]node_modules[\\/]/,
                        name: 'vendors',
                        chunks: 'all'
                    }
                }
            },
        },
        cache: mode === 'development' ? { type: 'filesystem' } : false,
        devtool: mode === 'development' ? 'source-map' : undefined,
            plugins: [
            ...(
                target === 'client' ? 
                [
                    new HtmlWebpackPlugin({
                        template: path.join(__dirname, 'src', 'index.html'),
                    })
                ] : 
                []
            ),
            new CleanWebpackPlugin({
                cleanOnceBeforeBuildPatterns: [`${target}/**/*`]
            }),
            // new WebpackManifestPlugin(),
            new DefinePlugin(JSON.stringify({
                'process.env.ENVIRONMENT': mode
            })),
        ],
    }
}