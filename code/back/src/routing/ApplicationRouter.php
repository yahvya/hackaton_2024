<?php

namespace Routing;

use Throwable;

/**
 * @brief application router
 */
class ApplicationRouter{
    /**
     * @brief manage application routing
     * @param string $route current route
     * @param array<string,array<string,array<string,string>>> $routesMap route maps, with the request method as key, pointing to an array indexed by the link and the treatment callable as value
     * @return never
     */
    public static function quickRouting(string $route,array $routesMap):never{
        $formattedRequestMethod = strtolower(string: $_SERVER["REQUEST_METHOD"]);
        $potentialRoutes = $routesMap[$formattedRequestMethod] ?? [];

        if(!array_key_exists(key: $route,array: $potentialRoutes))
            static::notFoundResponse();

        try{
            $potentialRoutes[$route][0] = new $potentialRoutes[$route][0]();
            call_user_func(callback: $potentialRoutes[$route]);
            die();
        }
        catch(Throwable){
            static::internalError();
        }
    }

    /**
     * @brief render not found response
     * @return never
     */
    public static function notFoundResponse():never{
        http_response_code(response_code: 404);
        die();
    }

    /**
     * @brief render internal error response
     * @return never
     */
    public static function internalError():never{
        http_response_code(response_code: 500);
        die();
    }

    /**
     * @brief render unauthorized response
     * @param array $message json message
     * @return never
     */
    public static function unauthorized(array $message = []):never{
        header(header: "Content-Type: application/json");
        http_response_code(response_code: 401);
        die(json_encode(value: $message,flags: JSON_PRETTY_PRINT));
    }
}