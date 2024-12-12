<?php

namespace Controllers;

use PdfPseudoApp\Utils\Security;
use Routing\ApplicationRouter;

/**
 * @brief abstract controller
 */
abstract class AbstractController{
    public function __construct(){
        if(!Security::checkSecurity())
            ApplicationRouter::unauthorized();
    }

    /**
     * @brief render a json content
     * @param array $json json content
     * @return never
     */
    public function renderJson(array $json):never{
        header(header: "Content-Type: application/json");
        http_response_code(response_code: 200);
        die(json_encode(value: $json,flags: JSON_PRETTY_PRINT));
    }
}