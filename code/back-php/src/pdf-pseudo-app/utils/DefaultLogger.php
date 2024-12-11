<?php

namespace PdfPseudoApp\Utils;

use Override;

/**
 * @brief pdf pseudo app default logger
 * @attention this logger will write the logs in a log file
 */
class DefaultLogger implements Logger{
    /**
     * @param string $logFileAbsolutePath log file absolute path
     */
    public function __construct(
        public readonly string $logFileAbsolutePath
    ){}

    #[Override]
    public function log(string $message): void{
        $currentTimestamp = time();
        file_put_contents(
            filename: $this->logFileAbsolutePath,
            data: "$currentTimestamp : $message\n",
            flags: FILE_APPEND
        );
    }
}