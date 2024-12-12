<?php

namespace PdfPseudoApp\Utils;

/**
 * @brief security manager
 */
abstract class Security{
    /**
     * @brief security checker
     * @return bool if the access is granted
     */
    public static function checkSecurity():bool{
        return true;
    }
}