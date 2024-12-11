<?php

namespace PdfPseudoApp\App;

use PdfPseudoApp\Utils\Logger;
use Throwable;

/**
 * @brief pdf pseudo app manager
 */
class PdfPseudoApp{
    /**
     * @param string $pdfFilePath pdf file path
     * @param Logger|null $logger logger
     */
    public function __construct(
        public readonly string $pdfFilePath,
        public readonly string $pythonScriptPath,
        public readonly ?Logger $logger = null
    ){}

    public function getEntitiesToTransform():void{
        die(shell_exec(command: "python3 $this->pythonScriptPath $this->pdfFilePath"));
        die("ici");
    }

    /**
     * @brief check if the provided uploaded file is secure from upload datas
     * @param array $fileData file data from php super global $_FILES[...]
     * @param Logger|null $logger log manager
     * @return bool if secure
     */
    public static function isUploadedFileSecure(array $fileData,?Logger $logger = null):bool{
        try{
            if($fileData["type"] !== "application/pdf")
                return false;

            $fileContent = @file_get_contents(filename: $fileData["tmp_name"], context: null,length:  4);

            if($fileContent === false || !str_starts_with(haystack: $fileContent,needle:  "%PDF"))
                return false;

            return true;
        }
        catch(Throwable $e){
            $logger?->log(message: $e->getMessage());

            return false;
        }
    }
}