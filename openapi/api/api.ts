/* tslint:disable */
/* eslint-disable */
/**
 * gaussian process regression api
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.0.1
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import { Configuration } from './configuration';
import globalAxios, { AxiosPromise, AxiosInstance, AxiosRequestConfig } from 'axios';
// Some imports not used depending on template conditions
// @ts-ignore
import { DUMMY_BASE_URL, assertParamExists, setApiKeyToObject, setBasicAuthToObject, setBearerAuthToObject, setOAuthToObject, setSearchParams, serializeDataIfNeeded, toPathString, createRequestFunction } from './common';
// @ts-ignore
import { BASE_PATH, COLLECTION_FORMATS, RequestArgs, BaseAPI, RequiredError } from './base';

/**
 * 
 * @export
 * @interface MlGetPredictionResponse
 */
export interface MlGetPredictionResponse {
    /**
     * 
     * @type {MlGetPredictionResponseResponse}
     * @memberof MlGetPredictionResponse
     */
    'response': MlGetPredictionResponseResponse;
}
/**
 * 
 * @export
 * @interface MlGetPredictionResponseResponse
 */
export interface MlGetPredictionResponseResponse {
    /**
     * 
     * @type {Array<MlGetPredictionResponseResponsePredictedData>}
     * @memberof MlGetPredictionResponseResponse
     */
    'predicted_data': Array<MlGetPredictionResponseResponsePredictedData>;
    /**
     * 
     * @type {MlGetPredictionResponseResponsePredictedData}
     * @memberof MlGetPredictionResponseResponse
     */
    'predicted_next_data': MlGetPredictionResponseResponsePredictedData;
}
/**
 * 
 * @export
 * @interface MlGetPredictionResponseResponsePredictedData
 */
export interface MlGetPredictionResponseResponsePredictedData {
    /**
     * 
     * @type {number}
     * @memberof MlGetPredictionResponseResponsePredictedData
     */
    'value': number;
    /**
     * 
     * @type {string}
     * @memberof MlGetPredictionResponseResponsePredictedData
     */
    'time': string;
    /**
     * 
     * @type {number}
     * @memberof MlGetPredictionResponseResponsePredictedData
     */
    'lower_bound': number;
    /**
     * 
     * @type {number}
     * @memberof MlGetPredictionResponseResponsePredictedData
     */
    'upper_bound': number;
}

/**
 * MlApi - axios parameter creator
 * @export
 */
export const MlApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * get predicted next data and predicted data
         * @summary get prediction data
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        mlPredictDelete: async (options: AxiosRequestConfig = {}): Promise<RequestArgs> => {
            const localVarPath = `/ml/predict`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'DELETE', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;


    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * MlApi - functional programming interface
 * @export
 */
export const MlApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = MlApiAxiosParamCreator(configuration)
    return {
        /**
         * get predicted next data and predicted data
         * @summary get prediction data
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async mlPredictDelete(options?: AxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<MlGetPredictionResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.mlPredictDelete(options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
    }
};

/**
 * MlApi - factory interface
 * @export
 */
export const MlApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = MlApiFp(configuration)
    return {
        /**
         * get predicted next data and predicted data
         * @summary get prediction data
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        mlPredictDelete(options?: any): AxiosPromise<MlGetPredictionResponse> {
            return localVarFp.mlPredictDelete(options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * MlApi - object-oriented interface
 * @export
 * @class MlApi
 * @extends {BaseAPI}
 */
export class MlApi extends BaseAPI {
    /**
     * get predicted next data and predicted data
     * @summary get prediction data
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof MlApi
     */
    public mlPredictDelete(options?: AxiosRequestConfig) {
        return MlApiFp(this.configuration).mlPredictDelete(options).then((request) => request(this.axios, this.basePath));
    }
}

