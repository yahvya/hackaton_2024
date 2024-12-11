<?php

namespace PdfPseudoApp\Utils;

/**
 * @brief pdf pseudo app internal logger
 */
interface Logger{
    /**
     * @brief log the provided message
     * @param string $message message
     * @return void
     */
    public function log(string $message):void;
}