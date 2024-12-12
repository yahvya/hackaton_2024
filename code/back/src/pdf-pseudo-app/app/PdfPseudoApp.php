<?php

namespace PdfPseudoApp\App;

use Exception;
use PdfPseudoApp\Utils\Logger;
use Throwable;

/**
 * @brief pdf pseudo app manager
 */
class PdfPseudoApp{
    /**
     * @param string $pdfFilePath pdf file path
     * @param string $pythonScriptPath python entities load script path
     * @param Logger|null $logger logger
     */
    public function __construct(
        public readonly string $pdfFilePath,
        public readonly string $pythonScriptPath,
        public readonly ?Logger $logger = null
    ){}

    /**
     * @brief search and provide the entities data to transform
     * @return array entities data
     * @throws Exception on error
     */
    public function getEntitiesToTransform():array{
        try{
            $commands = ["python3","python"];

            foreach($commands as $command){
                $entitiesData = @shell_exec(command: "$command $this->pythonScriptPath $this->pdfFilePath");

                if(!empty($entitiesData))
                    break;
            }

            $result = @json_decode(json: $entitiesData,associative: true);

            if(empty($result))
                throw new Exception(message: "Empty elements get received");

            return $result;
        }
        catch(Throwable $e){
            if($this->logger !== null)
                $this->logger->log(message: $e->getMessage());

            throw new Exception(message: "Fail to treat pdf");
        }
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